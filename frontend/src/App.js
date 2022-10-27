import "./css/App.css";
import React, { useState, useEffect } from "react";
import NameList from "./components/NameList";

const tableStyle = {
  borderRadius: "5px",
  margin: "10px",
  padding: "20px",
  boxShadow: "rgba(0, 0, 0, 0.24) 0px 3px 8px",
};

const wrapper = {
  width: "100%",
  paddingTop: "30px",
  marginLeft: "10px",
};

const buttonStyle = {
  padding: "5px",
  margin: "3px",
};

const pages = [1, 2, 3, 4, 5, 6, 7, 8];

function App() {
  const [index, setIndex] = useState(4);
  const [names, setNames] = useState([]);

  // useEffect for single rendering
  useEffect(() => {
    fetch(`/names/${index}`)
      .then((res) => res.json())
      .then((data) => {
        setNames(data);
      });
  }, [index]);

  const buttons = pages.map((pageNumber) => {
    return (
      <button key={pageNumber} onClick={() => setIndex(pageNumber)} style={buttonStyle}>
        {pageNumber}
      </button>
    );
  });
  return (
    <div>
      <div style={wrapper}>{buttons}</div>
      <div style={tableStyle}>
        <NameList key={names.id} names={names} />
      </div>
    </div>
  );
}

export default App;
