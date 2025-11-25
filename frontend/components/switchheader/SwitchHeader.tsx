'use client'

//select/chooseでは<HeaderSelect>を、それ以外は<Header>を使用する

import { usePathname } from 'next/navigation'
import Header from '../main/Header'
import HeaderSelect from '../main/select-main/HeaderSelect'

const SwitchHeader = () => {
  const pathName = usePathname();

  const isSelectPage = pathName.startsWith('/select/choose')
  return isSelectPage ? <HeaderSelect /> : <Header />
}

export default SwitchHeader