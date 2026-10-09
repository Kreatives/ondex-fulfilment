/* Injected in-page: flags text with (near-)invisible / low contrast vs its
   effective background. Writes JSON into #CONTRAST_REPORT[data-json]. */
(function () {
  function parse(c){ var m=(c||'').match(/[\d.]+/g); return m?m.map(Number):null; }
  function lum(rgb){ var v=rgb.slice(0,3).map(function(x){x/=255;return x<=.03928?x/12.92:Math.pow((x+.055)/1.055,2.4);}); return .2126*v[0]+.7152*v[1]+.0722*v[2]; }
  function ratio(a,b){ var la=lum(a),lb=lum(b),hi=Math.max(la,lb),lo=Math.min(la,lb); return (hi+.05)/(lo+.05); }
  function effBg(el){
    // Walk up tot de eerste OPAQUE solid achtergrond; noteer of er onderweg een
    // background-image/gradient zat (dan is de ratio een benadering).
    var onImg=false;
    function overMedia(node){ // positioned element bovenop een foto/video in zijn stacking-context
      var pos=getComputedStyle(node).position;
      if(pos==='absolute'||pos==='fixed'){
        var p=node.parentElement;
        while(p){ if(p.querySelector('img,video,picture,svg')) return true; var pp=getComputedStyle(p).position; if(pp!=='static') break; p=p.parentElement; }
      }
      return false;
    }
    while(el){ var cs=getComputedStyle(el);
      if(cs.backgroundImage && cs.backgroundImage!=='none') onImg=true;
      if((cs.backdropFilter&&cs.backdropFilter!=='none')||(cs.webkitBackdropFilter&&cs.webkitBackdropFilter!=='none')) onImg=true;
      if(overMedia(el)) onImg=true;
      var bg=parse(cs.backgroundColor);
      if(bg && (bg.length<4 || bg[3]>=0.85)) return {rgb:bg.slice(0,3), img:onImg};
      el=el.parentElement; }
    return {rgb:[255,255,255], img:onImg};
  }
  function ownText(el){
    var t='';
    for(var i=0;i<el.childNodes.length;i++){ if(el.childNodes[i].nodeType===3) t+=el.childNodes[i].textContent; }
    return t.trim();
  }
  var issues=[];
  var all=document.querySelectorAll('h1,h2,h3,h4,h5,h6,p,span,a,strong,small,li,button,b,em,td,th,label,figcaption,blockquote');
  all.forEach(function(el){
    var txt=ownText(el); if(txt.length<2) return;
    var cs=getComputedStyle(el);
    if(cs.visibility==='hidden'||cs.display==='none'||parseFloat(cs.opacity)<0.15) return;
    var r=el.getBoundingClientRect(); if(r.width<3||r.height<3) return;
    var color=parse(cs.color); if(!color) return;
    var bg=effBg(el);
    if(!bg.rgb){ return; } // bg is an image we can't sample; skip (manual)
    var cr=ratio(color, bg.rgb);
    var fs=parseFloat(cs.fontSize), fw=parseInt(cs.fontWeight)||400;
    var large=(fs>=24)||(fs>=18.66&&fw>=700);
    var need=large?3:4.5;
    if(cr<2.2 || cr<need){
      issues.push({t:txt.slice(0,46),tag:el.tagName,fs:Math.round(fs),fw:fw,color:cs.color,bg:'rgb('+bg.rgb.join(',')+')',onImg:bg.img,cr:Math.round(cr*100)/100,need:need,severity:cr<2.2?'INVISIBLE':'low'});
    }
  });
  // sort worst first
  issues.sort(function(a,b){return a.cr-b.cr;});
  var o=document.createElement('div'); o.id='CONTRAST_REPORT'; o.setAttribute('data-json', JSON.stringify(issues)); document.documentElement.appendChild(o);
})();
