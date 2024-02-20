import { BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import './App.css';
import Header from './Components/Header';
import Welcome from './Components/welcome';
import Graph from './Components/graph';

function App() {
  return (
    <div className="App">
      <Router>
        <Header />
        <Routes>
          <Route exact path='/home' element={<Welcome />} />
          <Route exact path='/graph' element={<Graph />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
