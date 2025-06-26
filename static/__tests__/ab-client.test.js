import { JSDOM } from 'jsdom';
import fs from 'fs';

const script = fs.readFileSync('../ab-client.js','utf8');

describe('variant assignment', () => {
  it('assigns variant to localStorage', () => {
    const dom = new JSDOM(`<!doctype html><button id="cta-test-btn">Join Now</button>`, { url: 'http://localhost' });
    const { window } = dom;
    window.fetch = jest.fn(() => Promise.resolve());
    const localStorage = window.localStorage;
    expect(localStorage.getItem('bl_ab_variant')).toBeNull();
    const func = new Function('window', script + '; return window.localStorage.getItem("bl_ab_variant");');
    func(window);
    expect(localStorage.getItem('bl_ab_variant')).not.toBeNull();
  });
});
