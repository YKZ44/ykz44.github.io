# -*- coding: utf-8 -*-
import io, json
m = json.load(io.open("manifest.json", encoding="utf-8"))
html = u'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>YKZ 試聴ページ</title>
<meta name="description" content="BOOTHで販売中のBGM・効果音素材の試聴ページ">
<style>
:root{--bg:#141220;--card:#1e1b2e;--text:#f1ecf4;--muted:#a79fb3;--accent:#ff9f5a;--accent2:#7fc3ff;--line:#2d2940}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"Hiragino Sans","Hiragino Kaku Gothic ProN","Noto Sans JP",sans-serif;line-height:1.5}
header{padding:28px 16px 8px;max-width:960px;margin:0 auto}h1{font-size:22px;margin:0 0 4px}header p{color:var(--muted);margin:0;font-size:14px}
main{max-width:960px;margin:0 auto;padding:12px 16px 60px;display:grid;gap:16px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px;display:grid;grid-template-columns:96px 1fr;gap:14px;scroll-margin-top:12px}
.card img{width:96px;height:96px;border-radius:10px;display:block}
.card h2{font-size:15px;margin:0 0 4px;line-height:1.35}.meta{color:var(--muted);font-size:13px;margin-bottom:8px}
.buy{display:inline-block;background:var(--accent);color:#1a1020;font-weight:700;text-decoration:none;padding:6px 12px;border-radius:8px;font-size:13px}
.player{grid-column:1/-1;display:flex;align-items:center;gap:10px;margin-top:4px}
.play{width:40px;height:40px;border-radius:50%;border:0;background:var(--accent2);color:#10131a;font-size:16px;cursor:pointer;flex:none}
.bar{flex:1;height:8px;background:var(--line);border-radius:4px;position:relative;cursor:pointer}.bar>i{position:absolute;left:0;top:0;height:100%;width:0;background:var(--accent2);border-radius:4px}
.time{font-variant-numeric:tabular-nums;color:var(--muted);font-size:12px;min-width:74px;text-align:right}
.tracks{grid-column:1/-1;display:grid;gap:4px;margin-top:6px}
.tr{display:flex;align-items:center;gap:8px;font-size:13px;padding:6px 8px;border-radius:8px;background:rgba(255,255,255,.03)}
.tr button{width:28px;height:28px;border-radius:50%;border:0;background:var(--line);color:var(--text);cursor:pointer;flex:none}.tr button.on{background:var(--accent)}
.tr .n{color:var(--muted);min-width:22px}.tr .d{margin-left:auto;color:var(--muted);font-size:12px}
.marks{grid-column:1/-1;display:flex;flex-wrap:wrap;gap:6px;margin-top:6px}.marks button{border:1px solid var(--line);background:transparent;color:var(--muted);border-radius:999px;padding:3px 9px;font-size:12px;cursor:pointer}.marks button.on{color:var(--text);border-color:var(--accent);background:rgba(255,159,90,.15)}
.note{grid-column:1/-1;font-size:12px;color:var(--muted)}
footer{max-width:960px;margin:0 auto;padding:0 16px 40px;color:var(--muted);font-size:12px}
@media(max-width:480px){.card{grid-template-columns:72px 1fr}.card img{width:72px;height:72px}}
</style></head><body>
<header><h1>YKZ 試聴ページ</h1><p>BOOTHで販売中のBGM・効果音素材のプレビューです。購入は各「BOOTHで購入」から。試聴音源は短く・低音質に加工してあります。</p></header>
<main>
'''
for e in m:
    kind = {'bgm': u'BGM素材（AI生成・Suno）', 'loop': u'ループ素材', 'sfx': u'効果音'}[e['kind']]
    html += u'<section class="card" id="%s"><img src="img/%s.jpg" alt=""><div><h2>%s</h2><div class="meta">%s ・ ¥%s ・ %d%s</div><a class="buy" href="%s" target="_blank" rel="noopener">BOOTHで購入 ↗</a></div>' % (e['key'], e['key'], e['title'], kind, format(e['price'], ','), e['n'], u'曲' if e['kind'] == 'bgm' else u'音', e['url'])
    html += u'<div class="player" data-src="audio/%s"><button class="play" aria-label="再生">▶</button><div class="bar"><i></i></div><span class="time">0:00 / %d:%02d</span></div>' % (e['digest']['file'], e['digest']['sec'] // 60, e['digest']['sec'] % 60)
    if e.get('tracks'):
        html += u'<div class="tracks">'
        for i, t in enumerate(e['tracks']):
            html += u'<div class="tr" data-src="audio/%s"><button aria-label="再生">▶</button><span class="n">%02d</span><span>%s</span><span class="d">試聴%ds / 本編%d:%02d</span></div>' % (t['file'], i + 1, t['label'], int(t['sec']), t['full'] // 60, t['full'] % 60)
        html += u'</div><div class="note">上のプレイヤーは全曲ダイジェスト。各曲18秒の抜粋です。</div>'
    if e.get('marks'):
        html += u'<div class="marks">' + u''.join(u'<button data-t="%s">%s</button>' % (k['t'], k['label']) for k in e['marks']) + u'</div><div class="note">タップで該当の音から再生（各1.6秒・モノラル96kbpsの試聴版）。</div>'
    html += u'</section>\n'
html += u'''</main>
<footer>© YKZ ・ 試聴音源の転載・二次利用は禁止 ・ <a href="https://ykz.booth.pm/" style="color:var(--accent2)">ykz.booth.pm</a></footer>
<script>
(function(){
const a=new Audio();let cur=null;const fmt=s=>Math.floor(s/60)+':'+String(Math.floor(s%60)).padStart(2,'0');
function stopUI(){document.querySelectorAll('.play').forEach(b=>b.textContent='▶');document.querySelectorAll('.tr button,.marks button').forEach(b=>b.classList.remove('on'));}
function play(src,ui,seek){if(cur!==src){a.src=src;cur=src;}if(seek!=null)a.currentTime=seek;a.play();stopUI();ui&&ui();}
document.querySelectorAll('.player').forEach(p=>{const b=p.querySelector('.play'),bar=p.querySelector('.bar'),fill=bar.querySelector('i'),tm=p.querySelector('.time'),src=p.dataset.src;
 b.addEventListener('click',()=>{if(cur===src&&!a.paused){a.pause();b.textContent='▶';return;}play(src,()=>b.textContent='⏸');});
 bar.addEventListener('click',ev=>{const r=bar.getBoundingClientRect();const f=(ev.clientX-r.left)/r.width;if(cur!==src){play(src,()=>b.textContent='⏸');a.addEventListener('loadedmetadata',()=>{a.currentTime=f*a.duration},{once:true});}else{a.currentTime=f*a.duration;}});
 a.addEventListener('timeupdate',()=>{if(cur!==src)return;const d=a.duration||0;fill.style.width=(d?100*a.currentTime/d:0)+'%';tm.textContent=fmt(a.currentTime)+' / '+fmt(d);});
 a.addEventListener('ended',()=>{if(cur===src){b.textContent='▶';fill.style.width='0';}});
 const sec=p.closest('.card');sec.querySelectorAll('.marks button').forEach(mb=>mb.addEventListener('click',()=>{const t=parseFloat(mb.dataset.t);if(cur!==src){play(src,()=>{b.textContent='⏸';mb.classList.add('on')});a.addEventListener('loadedmetadata',()=>{a.currentTime=t},{once:true});}else{play(src,()=>{b.textContent='⏸';mb.classList.add('on')},t);}}));
});
document.querySelectorAll('.tr').forEach(t=>{const b=t.querySelector('button'),src=t.dataset.src;b.addEventListener('click',()=>{if(cur===src&&!a.paused){a.pause();b.classList.remove('on');return;}play(src,()=>b.classList.add('on'));});a.addEventListener('ended',()=>{if(cur===src)b.classList.remove('on');});});
})();
</script></body></html>'''
io.open("index.html", "w", encoding="utf-8").write(html); print("index.html", len(html))
