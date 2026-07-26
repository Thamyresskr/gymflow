import { Outlet } from "react-router-dom";

import Header from "../components/layout/Header";
import Sidebar from "../components/layout/Sidebar";

import "./MainLayout.css";

function MainLayout() {
  return (
    <div className="layout">
      <Sidebar />

      <div className="layout-content">
        <Header />

        <main className="page-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

export default MainLayout;