import SidebarSelect from '@/components/main/select-main/SidebarSelect';
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
