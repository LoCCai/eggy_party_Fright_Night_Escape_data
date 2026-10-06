#!/usr/bin/env python3
"""
NeoX NXPK zstd-frame walker.
The encrypted file table cannot be decrypted (key in native lib), but the data
region of gameplay .npk files is a contiguous sequence of zstd frames (each
frame carries its own Frame_Content_Size), so files can be extracted by
chaining frame boundaries -- bypassing the table entirely.
"""
import struct, sys, os, io, json
import compression.zstd as zstd

def classify(out: bytes):
    if out[:4] == b'\xabKTX 11' or out[1:4] == b'KTX': return 'ktx'
    if out[:4] == b'\x34\x80\xc8\xbb': return 'mesh'
    if out[:7] == b'<NeoX\n' or out[:5] == b'<NeoX': return 'neox_xml'
    if out[:4] == b'\xc1YA\r': return 'anim_cfg'
    if out[:8] == b'AnimParam'[:8] or out[:9] == b'AnimParam': return 'anim_param'
    if out[:1] == b'{': return 'json'
    if out[:1] == b'<': return 'xml'
    if out[:4] == b'RIFF': return 'riff'
    if out[:4] == b'BKHD': return 'bnk'
    if out[:4] == b'OggS': return 'ogg'
    if out[:3] == b'PKM': return 'pkm'
    if out[:4] == b'\x89PNG': return 'png'
    if b'\x1bLua' in out[:16]: return 'lua'
    return 'bin'

def walk(path, outdir, scan_kw=None, max_frames=None, save_dir=None):
    fsize = os.path.getsize(path)
    f = open(path, 'rb')
    head = f.read(0x18)
    magic = head[:4]
    if magic != b'NXPK':
        print(f"{path}: not NXPK ({magic!r})"); return None
    count, = struct.unpack_from('<I', head, 4)
    map_off, = struct.unpack_from('<I', head, 0x14)
    data_end = min(map_off, fsize)
    print(f"== {os.path.basename(path)}: count={count} map_off={map_off:#x} file={fsize} "
          f"data={'COMPLETE' if fsize>=map_off else f'TRUNCATED({fsize}/{map_off})'} "
          f"table={'COMPLETE' if fsize >= map_off+count*28 else 'TRUNCATED(' + str(max(0,fsize-map_off)) + '/' + str(count*28) + 'B)'}")
    pos = 24  # skip header; frames start right after (check both 24 and 0)
    # find first frame: scan first 64 bytes for zstd magic
    f.seek(0)
    probe = f.read(4096)
    first = probe.find(b'\x28\xb5\x2f\xfd')
    if first < 0:
        print("   no zstd frames in first 4KB — data likely encrypted/different codec")
        return None
    pos = first
    stats = {}
    kw_hits = {}
    manifest = []
    n = 0
    f.seek(pos)
    CHUNK = 4*1024*1024
    buf = b''
    buf_start = pos
    while pos < data_end:
        if max_frames and n >= max_frames: break
        # ensure buffer has at least 32 bytes
        if len(buf) < 64:
            chunk = f.read(CHUNK)
            if not chunk: break
            buf = buf + chunk if buf else chunk
        m = buf.find(b'\x28\xb5\x2f\xfd')
        if m < 0:
            buf = buf[-8:]; buf_start = f.tell() - len(buf); continue
        try:
            fsz = zstd.get_frame_size(buf[m:])
        except Exception as e:
            # maybe truncated tail buffer; refill
            chunk = f.read(CHUNK)
            if not chunk:
                break
            buf = buf[m:] + chunk
            buf_start += m
            continue
        while len(buf) < m + fsz:
            chunk = f.read(max(CHUNK, m+fsz-len(buf)))
            if not chunk: break
            buf = buf + chunk
        if len(buf) < m + fsz:
            manifest.append({"idx": n, "off": buf_start+m, "size": fsz, "status": "truncated"})
            break
        try:
            out = zstd.decompress(buf[m:m+fsz])
        except Exception as e:
            stats['decomp_fail'] = stats.get('decomp_fail',0)+1
            manifest.append({"idx": n, "off": buf_start+m, "size": fsz, "status": "fail", "err": str(e)[:80]})
            buf = buf[m+fsz:]; buf_start += m+fsz
            n += 1
            continue
        typ = classify(out)
        stats[typ] = stats.get(typ,0)+1
        rec = {"idx": n, "off": buf_start+m, "fsize": fsz, "out": len(out), "type": typ, "status": "ok"}
        if save_dir and typ in ('neox_xml','json','xml','anim_cfg','anim_param','txt','bin','lua'):
            if len(out) < 8_000_000:
                fn = f"{save_dir}/{n:07d}_{typ}_{os.path.basename(path).replace('.npk','')}.bin"
                open(fn,'wb').write(out)
                rec['file'] = os.path.basename(fn)
        if scan_kw:
            for kw in scan_kw:
                if kw.encode('utf-8') in out:
                    kw_hits.setdefault(kw, []).append(n)
                    rec['kw'] = kw
        manifest.append(rec)
        buf = buf[m+fsz:]
        buf_start += m+fsz
        pos = buf_start
        n += 1
    print("   frames:", n, "types:", stats)
    if scan_kw:
        print("   KW hits:", {k: (len(v), v[:8]) for k, v in kw_hits.items()})
    return {"count_hdr": count, "map_off": map_off, "fsize": fsize, "frames": n,
            "types": stats, "kw": kw_hits, "manifest": manifest}

if __name__ == '__main__':
    path, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    kws = sys.argv[3].split(',') if len(sys.argv) > 3 and sys.argv[3] else None
    save = os.path.join(outdir, 'files')
    os.makedirs(save, exist_ok=True)
    r = walk(path, outdir, scan_kw=kws, save_dir=save)
    if r:
        base = os.path.basename(path).replace('.npk','').replace('.orbit.tmp','')
        json.dump(r, open(f"{outdir}/{base}.walk.json",'w'), ensure_ascii=False)
