import { RouterProvider, createBrowserRouter } from "react-router-dom";
import LandingPage from "./page/LandingPage";
import PricingPage from "./page/PricingPage";
import DocsPage from "./page/DocsPage";
import AuthPage from "./page/AuthPage";

const router = createBrowserRouter([
  {
    path: "/",
    element: <LandingPage/>,
  },
  {
    path: "/pricing",
    element: <PricingPage/>,
  },
  {
    path: "/docs",
    element: <DocsPage/>,
  },
  {
    path: "/login",
    element: <AuthPage/>,
  },
]);

export default function App() {
  return (
    <div className="h-screen bg-gradient-to-br from-gray-900 to-gray-600 bg-gradient-to-r text-gray-100 ">
        <RouterProvider router={router} />
    </div>    
  )
}