import { Route, Routes } from "react-router-dom";

import LoginPage from "@/pages/login";
import OverviewPage from "@/pages/overview";
import CampaignPage from "@/pages/campaigns";
import BlogPage from "@/pages/blog";
import AboutPage from "@/pages/about";
function App() {
  return (
    <Routes>
      <Route element={<LoginPage />} path="/" />
      <Route element={<OverviewPage />} path="/overview" />
      <Route element={<CampaignPage />} path="/campaigns" />
      <Route element={<BlogPage />} path="/blog" />
      <Route element={<AboutPage />} path="/about" />
    </Routes>
  );
}

export default App;
