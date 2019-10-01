import React from 'react';
import './App.css';
import { BrowserRouter as Router, Route } from "react-router-dom";

// Components
import SideBar from './components/SideBar/Sidebar';

import { makeStyles, useTheme } from '@material-ui/core/styles';


function Home(props: {}) {
  return (
    <div style={{ "color": "white" }}>
      <h1>Cameras here</h1>
    </div>
  )
}

function Stats(props: {}) {
  return (
    <div style={{ "color": "white" }}>
      <h1>Stats here</h1>
    </div>
  )
}

function Analysis(props: {}) {
  return (
    <div style={{ "color": "white" }}>
      <h1>Analysis here</h1>
    </div>
  )
}

function Playback(props: {}) {
  return (
    <div style={{ "color": "white" }}>
      <h1>Playback here</h1>
    </div>
  )
}

const drawerWidth = 240;

const useStyles = makeStyles(theme => ({
  root: {
    display: 'flex',
  },
  content: {
    marginLeft: '10px',
  },
}));

const App: React.FC = () => {
  const classes = useStyles();
  return (
    <div className="App">
      <Router>
        <div className={classes.root}>
          <SideBar />
          <Route exact path="/" component={Home} />
          
          <div className={classes.content} >
            <Route path="/cameras" component={Home} />
          </div>

          <div className={classes.content} >
            <Route path="/stats" component={Stats} />
          </div>

          <div className={classes.content} >
            <Route path="/analysis" component={Analysis} />
          </div>

          <div className={classes.content} >
            <Route path="/playback" component={Playback} />
          </div>
        </div>
      </Router>
    </div>
  );
}

export default App;
