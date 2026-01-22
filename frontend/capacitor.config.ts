import type { CapacitorConfig } from '@capacitor/cli'

const config: CapacitorConfig = {
  appId: 'com.example.mobileapp',
  appName: 'Mobile App',
  webDir: 'dist',
  server: {
    // En desarrollo, usar servidor local
    // url: 'http://192.168.1.100:5173',
    cleartext: true
  },
  plugins: {
    SplashScreen: {
      launchShowDuration: 2000,
      backgroundColor: '#42b883',
      showSpinner: false
    },
    StatusBar: {
      style: 'dark',
      backgroundColor: '#42b883'
    }
  }
}

export default config
