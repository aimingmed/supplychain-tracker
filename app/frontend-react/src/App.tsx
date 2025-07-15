import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import {
  ProductManagement,
  InventoryManagement,
  TaskManagement,
  DemandManagement,
  MaterialManagement,
  ScrapManagement
} from './pages';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Navigate to="/product-management" replace />} />
            <Route path="/product-management" element={<ProductManagement />} />
            <Route path="/inventory-management" element={<InventoryManagement />} />
            <Route path="/task-management" element={<TaskManagement />} />
            <Route path="/demand-management" element={<DemandManagement />} />
            <Route path="/material-management" element={<MaterialManagement />} />
            <Route path="/scrap-management" element={<ScrapManagement />} />
          </Route>
        </Routes>
      </div>
    </Router>
  );
}

export default App
