import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import  Select from '@mui/material/Select'
import MenuItem from '@mui/material/MenuItem'
import { useState, useEffect } from 'react';
import axios from "axios"
import AirportTableRow from './AirportTableRow';


export default function AirportTable() {
  
  
  const [rows, setRows] = useState([{}])
  const [filter, setFilter] = useState('All')
  const [serverRows, setServerRows] = useState([{}])

  

  useEffect(()=> {
    axios.get("http://localhost:8000/api/all",{mode:'no-cors'})
      .then((response) => {        
        let rows =[]
        response.data.data.forEach(airport => {
          let row = {}
          row.iata = airport.fields.iata_code
          row.city = airport.fields.city
          row.state = airport.fields.state
          row.status = airport.fields.status
          row.latitude = airport.fields.lat
          row.longitude = airport.fields.lon
          row.reason = airport.fields.reason
          rows.push(row)          
        });

        setServerRows(rows)
      })   
  },[])
  
  useEffect(()=>{
    if (filter === "All"){
      setRows(serverRows)
    } else {
      setRows(serverRows.filter(obj => obj.status === filter))
    }

  },[serverRows,filter])

    function handleSelectChange(event){
      setFilter(event.target.value)   
    }

  return (
    <div style={{display:'flex', flexDirection: 'column', padding: '25px'}}>
    <h1>Manage Airports</h1>
    <Select style={{alignSelf: 'center', width : '200px'}}
    labelId="Status"
    id="demo-simple-select"
    value={filter}
    label="Status"
    onChange={handleSelectChange}
  >
    <MenuItem value={'All'}>All</MenuItem>
    <MenuItem value={'A'}>Active</MenuItem>
    <MenuItem value={'I'}>Inactive</MenuItem>
  </Select>
   <div className="Table-container"> 
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>IATA</TableCell>
            <TableCell align="right">City</TableCell>
            <TableCell align="right">State&nbsp;(g)</TableCell>
            <TableCell align="right">Latitude</TableCell>
            <TableCell align="right">Longitude</TableCell>
            <TableCell align="right">Reason Deactivation</TableCell>            
            <TableCell align="right">Activated</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <AirportTableRow
              key = {row.iata} 
              iata={row.iata} 
              city={row.city} 
              state={row.state} 
              latitude={row.latitude}
              longitude={row.longitude}
              reason = {row.reason}
              status = {row.status}
            />
          ))}
        </TableBody>
      </Table>
    </TableContainer>
    </div>
    </div>
  );
}