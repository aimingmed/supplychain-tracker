import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Layout from './components/Layout';
import {
  Login,
  ProductManagement,
  InventoryManagement,
  TaskManagement,
  DemandManagement,
  MaterialManagement,
  ScrapManagement,
  UserProfile
} from './pages';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/" element={
              <ProtectedRoute>
                <Layout />
              </ProtectedRoute>
            }>
              <Route index element={<Navigate to="/product-management" replace />} />
              <Route path="/product-management" element={<ProductManagement />} />
              <Route path="/inventory-management" element={<InventoryManagement />} />
              <Route path="/task-management" element={<TaskManagement />} />
              <Route path="/demand-management" element={<DemandManagement />} />
              <Route path="/material-management" element={<MaterialManagement />} />
              <Route path="/scrap-management" element={<ScrapManagement />} />
              <Route path="/profile" element={<UserProfile />} />
            </Route>
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App
