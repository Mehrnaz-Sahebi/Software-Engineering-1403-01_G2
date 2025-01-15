import { Suspense } from "react";
import Fallback from "./components/fallback/Fallback";
import { createBrowserRouter } from "react-router-dom";
import HeaderLayout from "./components/Header/HeaderLayout";
import App from "./App";
import SynonymChecker from "./components/SynonymChecker/SynonymChecker";
import NotFound from "./components/NotFound/NotFound";
import Aboutus from "./components/Aboutus/Aboutus";
import Login from "./components/Login/Login";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      {
        path: "/",
        element: <HeaderLayout></HeaderLayout>,
        children: [
          {
            path: "/",
            element: (
              <Suspense fallback={<Fallback />}>
                <SynonymChecker />
              </Suspense>
            ),
          },
          {
            path: "/about",
            element: (
              <Suspense fallback={<Fallback />}>
                <Aboutus />
              </Suspense>
            ),
          },
          {
            path: "/login",
            element: (
              <Suspense fallback={<Fallback />}>
                <Login />
              </Suspense>
            ),
          },

          {
            path: "*",
            element: <NotFound />,
          },
        ],
      },
    ],
  },
]);

export default router;
