# BroIsThisFake - React Frontend

Modern React + TailwindCSS frontend with glassmorphism design for the fake banking app detector.

## Features

- 🎨 **Liquid Glass Design** - Beautiful glassmorphism UI with frosted effects
- 📱 **Fully Responsive** - Works on all screen sizes
- ⚡ **Fast & Modern** - Built with Vite and React 18
- 🎯 **Component-Based** - Reusable glass components

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

3. Make sure the backend is running on `http://localhost:5000`

## Project Structure

```
frontend-react/
├── src/
│   ├── components/
│   │   ├── Sidebar.jsx
│   │   ├── Header.jsx
│   │   ├── GlassCard.jsx
│   │   ├── GlassButton.jsx
│   │   ├── AnalyzePanel.jsx
│   │   └── DetectionFeed.jsx
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── package.json
├── vite.config.js
└── tailwind.config.js
```

## Design Features

- **Glassmorphism**: Frosted glass effects with backdrop blur
- **Gradient Backgrounds**: Beautiful purple/indigo gradients
- **Smooth Animations**: Hover effects and transitions
- **Responsive Sidebar**: Collapses on mobile
- **Glass Cards**: Translucent cards with inner glow
- **Glass Buttons**: Interactive buttons with hover effects

## Build for Production

```bash
npm run build
```

The built files will be in the `dist` folder.

