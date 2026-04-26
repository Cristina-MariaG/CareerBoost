<template>
  <div class="app">
    <div class="bg-mesh">
      <div class="blob b1"></div>
      <div class="blob b2"></div>
      <div class="blob b3"></div>
    </div>

    <header class="header">
      <div class="logo">
        <div class="logo-icon">🚀</div>
        Career<span class="logo-accent">Boost</span> <span class="logo-ia">IA</span>
      </div>
      <nav class="nav">
        <router-link class="nav-btn" to="/linkedin" active-class="nav-btn--active">LinkedIn Post</router-link>
        <router-link class="nav-btn" to="/cv" active-class="nav-btn--active">CV &amp; Lettre</router-link>
      </nav>
    </header>

    <main class="main">
      <router-view />
    </main>
  </div>
</template>

<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --cyan: #00E5FF;
  --violet: #8B5CF6;
  --pink: #F472B6;
  --bg: #080B14;
  --card: #151C2E;
  --card2: #1C2540;
  --text: #F0F4FF;
  --text-muted: #8B95B0;
  --text-body: #C9D1E0;
  --fh: 'Inter', sans-serif;
  --fb: 'Inter', sans-serif;
}

html, body {
  background: var(--bg);
  color: var(--text);
  font-family: var(--fb);
  min-height: 100vh;
}
</style>

<style scoped>
.app {
  min-height: 100vh;
  position: relative;
}

.bg-mesh {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
}
.blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.09;
}
.b1 { width: 600px; height: 600px; background: #8B5CF6; top: -200px; right: -100px; animation: d1 12s ease-in-out infinite; }
.b2 { width: 500px; height: 500px; background: #00E5FF; bottom: -100px; left: -150px; animation: d2 15s ease-in-out infinite; }
.b3 { width: 280px; height: 280px; background: #F472B6; top: 40%; left: 32%; animation: d3 10s ease-in-out infinite; }
@keyframes d1 { 0%,100%{transform:translate(0,0)} 50%{transform:translate(-35px,25px)} }
@keyframes d2 { 0%,100%{transform:translate(0,0)} 50%{transform:translate(30px,-35px)} }
@keyframes d3 { 0%,100%{transform:translate(0,0)} 50%{transform:translate(-18px,18px)} }

.header {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 10;
  padding: 16px 40px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid rgba(255,255,255,0.1);
  backdrop-filter: blur(20px);
  background: rgba(8,11,20,0.92);
}

.logo {
  font-family: var(--fh);
  font-size: 17px;
  font-weight: 800;
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--text);
  text-decoration: none;
}
.logo-icon {
  width: 30px;
  height: 30px;
  border-radius: 8px;
  background: linear-gradient(135deg, var(--cyan), var(--violet));
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 15px;
}
.logo-accent {
  background: linear-gradient(135deg, var(--cyan), var(--violet));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.logo-ia {
  font-size: 12px;
  font-weight: 700;
  color: var(--text-muted);
  letter-spacing: 0.05em;
}

.nav {
  display: flex;
  gap: 3px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 100px;
  padding: 4px;
}
.nav-btn {
  background: transparent;
  border: none;
  color: var(--text-muted);
  font-family: var(--fb);
  font-size: 13px;
  font-weight: 600;
  padding: 7px 16px;
  border-radius: 100px;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
}
.nav-btn:hover { color: #fff; background: rgba(255,255,255,0.08); }
.nav-btn--active {
  background: rgba(0,229,255,0.15);
  color: var(--cyan);
  border: 1px solid rgba(0,229,255,0.3);
}

.main {
  position: relative;
  z-index: 5;
  padding-top: 88px;
  min-height: 100vh;
}

@media (max-width: 620px) {
  .header { padding: 14px 16px; }
  .nav-btn { padding: 6px 10px; font-size: 12px; }
}
</style>
