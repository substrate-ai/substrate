import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/Auth';

import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu"
import React from 'react';
import { cn } from "@/lib/utils"
import { DropdownMenu, DropdownMenuContent, DropdownMenuGroup, DropdownMenuItem, DropdownMenuSeparator, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Badge } from "@/components/ui/badge"



function MainNavigation() {
  const { user } = useAuth()
  const { signOut } = useAuth()

  const handleLogout = () => {
    
    console.log('logout')
    signOut()
    // refresh the page to clear the cache
  }
  return (
    <NavigationMenu>
      <NavigationMenuList>
          <NavigationMenuItem>
                  <Link to="/">
                  <NavigationMenuLink className="font-bold px-5" href='/'>
                    {/* TODO add logo */}
                    <p className='inline px-2'>SubstrateAI</p>
                    
                    <Badge variant="outline">Beta</Badge>

                  </NavigationMenuLink>
                  </Link>
                  <>
                  
                  <Link to="https://docs.substrateai.com">
                  <NavigationMenuLink className={navigationMenuTriggerStyle()} href="https://docs.substrateai.com">
                    Documentation
                  </NavigationMenuLink>
                  </Link>

                  <Link to="pricing">
                  <NavigationMenuLink className={navigationMenuTriggerStyle()} href="pricing">
                    Pricing
                  </NavigationMenuLink>
                  </Link>

                  <Link to="blog">
                  <NavigationMenuLink className={navigationMenuTriggerStyle()} href="blog">
                    Blog
                  </NavigationMenuLink>
                  </Link>
          

                { user &&
                  <Link to="dashboard">
                    <NavigationMenuLink className={navigationMenuTriggerStyle()} href="dashboard">
                      Dashboard
                    </NavigationMenuLink>
                    </Link>

                }

                  </>

                { !user &&
                  <>  
                      <Link to="sign-up">
                      <NavigationMenuLink className={navigationMenuTriggerStyle()} href="sign-up">
                        Sign-up 
                      </NavigationMenuLink>
                      </Link>

                      <Link to="login">
                      <NavigationMenuLink className={navigationMenuTriggerStyle()} href="login">
                        Login 
                      </NavigationMenuLink>
                      </Link>
                  </>
                }

                {/* dropdown */}
                { user &&
                  <>
                
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="ghost" className="relative h-8 w-8 rounded-full">
                        <Avatar className="h-8 w-8">
                          {/* <AvatarImage src="/avatars/01.png" alt="avatar" /> */}
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
                        <Link to="/dashboard">
                        <DropdownMenuItem>
                          Dashboard
                        </DropdownMenuItem>
                        </Link>
                        {/* <DropdownMenuItem onClick={() => navigate("/settings")}>
                          Settings
                        </DropdownMenuItem> */}
                      </DropdownMenuGroup>
                      <DropdownMenuSeparator />
                      <DropdownMenuItem onClick={handleLogout} >
                        Log out
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                  </>
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
