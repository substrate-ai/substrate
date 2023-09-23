import { ReactNode } from 'react';
import MainNavigation from './MainNavigationBar';

function RootLayout({ children }: {children: ReactNode}) {
  return (
    <>
      <MainNavigation />
      <main>{children}</main>
      </>
  );
}

export default RootLayout;