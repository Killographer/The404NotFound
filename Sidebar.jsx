import React from 'react';
import { 
  FileText, 
  Upload, 
  Search, 
  History, 
  Settings,
  Shield 
} from 'lucide-react';

const Sidebar = ({ activeTab, onTabChange }) => {
  const menuItems = [
    { id: 'scan', icon: Search, label: 'Scan App', active: activeTab === 'scan' },
    { id: 'upload', icon: Upload, label: 'Upload APK', active: activeTab === 'upload' },
    { id: 'package', icon: FileText, label: 'Package Name', active: activeTab === 'package' },
    { id: 'history', icon: History, label: 'History', active: activeTab === 'history' },
    { id: 'settings', icon: Settings, label: 'Settings', active: activeTab === 'settings' },
  ];

  return (
    <aside className="glass-soft rounded-2xl p-4 md:p-6 h-fit md:sticky md:top-6">
      <div className="flex flex-col gap-2">
        <div className="flex items-center gap-3 mb-4 px-2">
          <Shield className="w-6 h-6 text-white" />
          <span className="text-white font-bold text-lg hidden md:block">Menu</span>
        </div>
        {menuItems.map((item) => {
          const Icon = item.icon;
          return (
            <button
              key={item.id}
              onClick={() => onTabChange(item.id)}
              className={`
                flex items-center gap-3 px-4 py-3 rounded-xl
                transition-all duration-300
                ${item.active 
                  ? 'glass-strong bg-white/25 border-white/40 shadow-lg' 
                  : 'glass-soft bg-white/10 border-white/20 hover:bg-white/15'
                }
                ${item.active ? 'scale-105' : 'hover:scale-105'}
              `}
            >
              <Icon className={`w-5 h-5 ${item.active ? 'text-white' : 'text-white/80'}`} />
              <span className={`font-semibold ${item.active ? 'text-white' : 'text-white/80'} hidden md:block`}>
                {item.label}
              </span>
            </button>
          );
        })}
      </div>
    </aside>
  );
};

export default Sidebar;

