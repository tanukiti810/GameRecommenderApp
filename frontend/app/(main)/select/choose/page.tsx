'use client';

import SidebarSelect from '@/components/main/select-main/SidebarSelect';
import '../../../globals.css';
import SelectedGames from '@/components/main/selected-games/SelectedGames';

const ChoosePage = () => {
  return (
    <div className='choosePage'>
      <SidebarSelect />
      <SelectedGames />
    </div>
  );
};

export default ChoosePage;
