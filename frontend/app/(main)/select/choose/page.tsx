'use client';

import SidebarSelect from '@/components/main/select-main/SidebarSelect';
import '../../../globals.css';

const ChoosePage = () => {
  return (
    <div className='choosePage'>
      <SidebarSelect />
      <div className='ChooseBox'>
        <h2>Genre Selection</h2>
        <p>Select genres from the sidebar to filter content.</p>
        
        {Array.from({ length: 50 }, (_, i) => (
          <div key={i} style={{ padding: '20px', marginBottom: '10px', background: '#fff', borderRadius: '4px' }}>
            Content Item {i + 1}
          </div>
        ))}
      </div>
    </div>
  );
};

export default ChoosePage;
