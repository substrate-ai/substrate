import { Link, NavLink, useNavigate } from 'react-router-dom';
import { IconButton, Nav, Navbar, Tag } from 'rsuite';
import HomeIcon from '@rsuite/icons/legacy/Home';
import { useAuth } from '../hooks/Auth';
import OffRoundIcon from '@rsuite/icons/OffRound';
import AdminIcon from '@rsuite/icons/Admin';
import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuIndicator,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
  NavigationMenuViewport,
  navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu"
import React from 'react';
import { cn } from "@/lib/utils"
import { DropdownMenu, DropdownMenuContent, DropdownMenuGroup, DropdownMenuItem, DropdownMenuSeparator, DropdownMenuShortcut, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { AvatarImage } from '@radix-ui/react-avatar';
import { DropdownMenuLabel } from '@radix-ui/react-dropdown-menu';


function MainNavigation() {
  const { user } = useAuth()
  const { signOut } = useAuth()

  const navigate = useNavigate()

  const handleLogout = () => {
    
    console.log('logout')
    signOut()
    // refresh the page to clear the cache
  }
  return (
    // <Navbar>
    //   <Nav>
    //     <Nav.Item to={'/'} as={NavLink} icon={<HomeIcon />}>Home</Nav.Item>
    //     <Nav.Item to={'/blog'} as={NavLink}>News</Nav.Item>
    //     {user ? (
    //       <Nav.Item as={NavLink} to="#">
    //         <IconButton size='sm' onClick={handleLogout} appearance='primary' icon={<OffRoundIcon />}>Logout</IconButton>
    //       </Nav.Item>
    //     ) : (
    //       <Nav.Item as={NavLink} to="/login">
    //         <Tag color="red">Not Logged In</Tag>
    //       </Nav.Item>
    //     )}
    //   </Nav>
    //   <Nav pullRight>
    //     {user && <Nav.Item icon={<AdminIcon />}><p>Welcome back {user?.email}</p></Nav.Item>}
    //   </Nav>
    // </Navbar>
    <NavigationMenu>
      <NavigationMenuList>
          <NavigationMenuItem>

                  <NavigationMenuLink className={navigationMenuTriggerStyle()} onClick={() => navigate("/docs")}>
                    Documentation
                  </NavigationMenuLink>

                {/* <a href={`/pricing`}> */}
                  <NavigationMenuLink className={navigationMenuTriggerStyle()} onClick={() => navigate("/pricing")}>
                    Pricing
                  </NavigationMenuLink>
          

                { user &&
                    <NavigationMenuLink className={navigationMenuTriggerStyle()}  onClick={() => navigate("/dashboard")}>
                      Dashboard
                    </NavigationMenuLink>

                }

                { !user &&
                  <>  
                      <NavigationMenuLink className={navigationMenuTriggerStyle()}  onClick={() => navigate("/login")}>
                        Sign-up 
                      </NavigationMenuLink>

                      <NavigationMenuLink className={navigationMenuTriggerStyle()} onClick={() => navigate("/login")}>
                        Login 
                      </NavigationMenuLink>
                  </>
                }

                { user &&
                  // name of the user 
                  
                  
                  <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" className="relative h-8 w-8 rounded-full">
          <Avatar className="h-8 w-8">
            <AvatarImage src="/avatars/01.png" alt="avatar" />
            <AvatarFallback>{user?.email?.substring(0, 2)}</AvatarFallback>
          </Avatar>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent className="w-56" align="end" forceMount>
        <DropdownMenuItem disabled>
          {user?.email}
        </DropdownMenuItem>
        <DropdownMenuSeparator />
        <DropdownMenuGroup>
          <DropdownMenuItem>
            Dashboard
          </DropdownMenuItem>
          <DropdownMenuItem>
            Settings
          </DropdownMenuItem>
          <DropdownMenuItem>New Team</DropdownMenuItem>
        </DropdownMenuGroup>
        <DropdownMenuSeparator />
        <DropdownMenuItem onClick={handleLogout} >
          Log out
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
                  
                }



                

                
        </NavigationMenuItem>
      </NavigationMenuList>
    </NavigationMenu>
  );
}

const ListItem = React.forwardRef<
  React.ElementRef<"a">,
  React.ComponentPropsWithoutRef<"a">
>(({ className, title, children, ...props }, ref) => {
  return (
    <li>
      <NavigationMenuLink asChild>
        <a
          ref={ref}
          className={cn(
            "block select-none space-y-1 rounded-md p-3 leading-none no-underline outline-none transition-colors hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground",
            className
          )}
          {...props}
        >
          <div className="text-sm font-medium leading-none">{title}</div>
          <p className="line-clamp-2 text-sm leading-snug text-muted-foreground">
            {children}
          </p>
        </a>
      </NavigationMenuLink>
    </li>
  )
})
ListItem.displayName = "ListItem"

export default MainNavigation;