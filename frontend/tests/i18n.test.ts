import { describe, it, expect } from 'vitest';
import i18n from '../src/locales/i18n';

describe('i18n configuration', () => {
  it('should initialize with zh as default language', () => {
    expect(i18n.language).toBe('zh');
  });

  it('should have translations for login', () => {
    expect(i18n.t('login')).toBe('登录');
    
    // Switch to English and test
    i18n.changeLanguage('en');
    expect(i18n.t('login')).toBe('Login');
  });
});
