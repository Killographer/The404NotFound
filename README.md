# Fake App Detector - Frontend

A modern, glassmorphism-styled React frontend for the Fake App Detector application.

## Features

- ✨ **Liquid Glass (Glassmorphism) Design** - Beautiful frosted glass UI with backdrop blur effects
- 🎨 **TailwindCSS** - Modern utility-first CSS framework
- ⚛️ **React 18** - Latest React with hooks
- 📱 **Fully Responsive** - Works on all device sizes
- 🎯 **Component-Based** - Reusable glassmorphism components
- 🚀 **Vite** - Fast build tool and dev server

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Sidebar.jsx      # Left sidebar navigation
│   │   ├── Header.jsx       # Top header component
│   │   ├── GlassCard.jsx    # Reusable glass card
│   │   └── GlassButton.jsx  # Reusable glass button
│   ├── App.jsx             # Main application component
│   ├── main.jsx             # React entry point
│   └── index.css            # TailwindCSS styles
├── index.html               # HTML template
├── package.json             # Dependencies
├── tailwind.config.js       # TailwindCSS configuration
├── postcss.config.js        # PostCSS configuration
└── vite.config.js           # Vite configuration
```

## Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## Development

Start the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:3000`

## Build

Create a production build:
```bash
npm run build
```

Preview the production build:
```bash
npm run preview
```

## Components

### GlassButton
A reusable button component with glassmorphism styling.

**Props:**
- `variant`: 'primary' | 'secondary' | 'ghost' (default: 'primary')
- `onClick`: Click handler function
- `disabled`: Boolean
- `className`: Additional CSS classes

### GlassCard
A reusable card component with glassmorphism styling.

**Props:**
- `padding`: 'none' | 'small' | 'default' | 'large' (default: 'default')
- `hover`: Boolean - enables hover effects
- `className`: Additional CSS classes

### Sidebar
Left sidebar navigation component with menu items.

**Props:**
- `activeTab`: Current active tab ID
- `onTabChange`: Function to handle tab changes

### Header
Top header component with title and subtitle.

**Props:**
- `title`: Header title text
- `subtitle`: Optional subtitle text

## Design Features

- **Glassmorphism Effects:**
  - Frosted translucent backgrounds (`bg-white/15`, `bg-white/20`, etc.)
  - Backdrop blur (`backdrop-blur-xl`, `backdrop-blur-2xl`)
  - Soft glowing borders (`border-white/30`)
  - Gradient overlays
  - Inner glow effects

- **Animations:**
  - Fade-in animations
  - Hover scale effects
  - Smooth transitions
  - Loading spinners

- **Responsive Design:**
  - Mobile-first approach
  - Breakpoints: `sm`, `md`, `lg`
  - Flexible grid layouts
  - Adaptive sidebar (sticky on desktop, normal on mobile)

## API Integration

The app connects to the backend API at `http://localhost:5000`:

- `POST /analyze_apk` - Analyze uploaded APK file
- `POST /analyze_package` - Analyze package name

Make sure the backend server is running before using the frontend.

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

Built for Pixel Pitch 2025 | BroIsThisFake

