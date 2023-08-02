import { ReactNode } from 'react';
import Navbar from './Navbar';

function RootLayout({ children }: {children: ReactNode}) {
  return (
    <>
      <Navbar />
      <main>{children}</main>
      </>
  );
}

export default RootLayout;