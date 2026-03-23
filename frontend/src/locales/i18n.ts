import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const resources = {
  en: {
    translation: {
      "login": "Login",
      "dashboard": "Dashboard",
      "drugs": "Drug List",
      "analysis": "Cost Analysis",
      "settings": "Settings",
      "theme": "Theme",
      "light": "Light",
      "dark": "Dark",
      "language": "Language"
    }
  },
  zh: {
    translation: {
      "login": "登录",
      "dashboard": "仪表板",
      "drugs": "药品列表",
      "analysis": "成本分析",
      "settings": "设置",
      "theme": "主题",
      "light": "亮色",
      "dark": "暗色",
      "language": "语言"
    }
  }
};

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: "zh",
    fallbackLng: "en",
    interpolation: {
      escapeValue: false
    }
  });

export default i18n;
