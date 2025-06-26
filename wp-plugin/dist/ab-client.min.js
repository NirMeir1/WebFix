(function(){
  if(!window.BL_AB_CONFIG||window.BL_AB_CONFIG.enabled!=='true') return;
  const EXP = 'cta_test';
  const VARIANTS = ['A','B','C'];
  const TEXTS = {
    'A': null,
    'B':'Get Started',
    'C':'Start Your Free Trial'
  };
  function chooseVariant(){
    let v = localStorage.getItem('bl_ab_variant');
    if(!v){
      v = VARIANTS[Math.floor(Math.random()*VARIANTS.length)];
      localStorage.setItem('bl_ab_variant', v);
    }
    return v;
  }
  const variant = chooseVariant();
  document.querySelectorAll('[data-ab-id="cta"]')
    .forEach(el=>{ if(TEXTS[variant]) el.textContent = TEXTS[variant]; });
  function track(goal){
    fetch('https://localhost:8001/events',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({experiment:EXP,variant,goal})
    });
  }
  track('view');
  document.querySelectorAll('[data-ab-id="cta"]').forEach(el=>{
    el.addEventListener('click',()=>track('cta_click'));});
})();
