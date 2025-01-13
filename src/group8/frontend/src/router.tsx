import { Suspense } from "react";
import Fallback from "./components/fallback/Fallback";
import { createBrowserRouter } from "react-router-dom";
import HeaderLayout from "./components/Header/HeaderLayout";
import App from "./App";
import SynonymChecker from "./components/SynonymChecker/SynonymChecker";

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
            path: "/synonymChecker",
            element: (
              <Suspense fallback={<Fallback />}>
                <SynonymChecker></SynonymChecker>
              </Suspense>
            ),
          },
        ],
      },
    ],
  },
]);

export default router;
