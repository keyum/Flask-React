const tableStyle = {
  fontFamily: "Arial, Helvetica, sansSerif",
  width: "100%",
  borderCollapse: "collapse",
  border: "1px solid #ddd",
  padding: "10px",
};

const headerStyle = {
  paddingTop: "12px",
  paddingBottom: "12px",
  textAlign: "center",
  backgroundColor: "#04AA6D",
  color: "white",
};

const rowStyle = {
  border: "1px solid #ddd",
};

const tdStyle = {
  padding: "5px 20px",
  color: "black",
  fontWeight: "normal",
};

const NameList = ({ names }) => {
  return (
    <table style={tableStyle}>
      <thead>
        <tr style={rowStyle}>
          <th style={headerStyle}>Name</th>
        </tr>
      </thead>
      <tbody>
        {names.map((each, index) => (
          <tr style={rowStyle} key={index}>
            <td style={tdStyle}>{each}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default NameList;
