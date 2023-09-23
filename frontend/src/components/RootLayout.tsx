import { ReactNode } from 'react';
import { MainNavigationBar } from './MainNavigationBar';

export function RootLayout({ children }: {children: ReactNode}) {
  return (
    <>
      <MainNavigationBar />
      <main>{children}</main>
    </>
  );
}
