import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
} from "react-router-dom";

import ProtectedRoute from "../components/auth/ProtectedRoute";
import MainLayout from "../layouts/MainLayout";

import Login from "../pages/Login/Login";
import Dashboard from "../pages/Dashboard/Dashboard";
import Users from "../pages/Users/Users";
import Checkins from "../pages/Checkins/Checkins";

function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Rotas Públicas */}
        <Route
          path="/login"
          element={<Login />}
        />

        {/* Rotas Protegidas */}
        <Route element={<ProtectedRoute />}>
          <Route element={<MainLayout />}>
            <Route
              path="/dashboard"
              element={<Dashboard />}
            />

            <Route
              path="/users"
              element={<Users />}
            />

            <Route
              path="/checkins"
              element={<Checkins />}
            />
          </Route>
        </Route>

        {/* Redirecionamento */}
        <Route
          path="*"
          element={<Navigate to="/dashboard" replace />}
        />
      </Routes>
    </BrowserRouter>
  );
}

export default AppRoutes;