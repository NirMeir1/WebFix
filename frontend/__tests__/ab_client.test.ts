import { JSDOM } from 'jsdom';

function bucket() {
  const variants = ['A','B','C'];
  let v = localStorage.getItem('bl_ab_variant');
  if(!v){
    v = variants[Math.floor(Math.random()*variants.length)];
    localStorage.setItem('bl_ab_variant', v);
  }
  return v;
}

test('assigns persistent variant', () => {
  const dom = new JSDOM('', { url: 'https://localhost' });
  // @ts-ignore
  global.window = dom.window;
  const first = bucket();
  const second = bucket();
  expect(first).toBe(second);
});
