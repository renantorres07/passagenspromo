import React from 'react';
import { useState} from 'react';
import TableCell from '@mui/material/TableCell';
import MySwitch from './MySwitch';
import TableRow from '@mui/material/TableRow';

export default function AirportTableRow(props){

	const {iata,city,state,latitude,longitude,reason,status} = props
	const [reasonInactive,setReasonInactive] = useState(reason)

	return (
		<TableRow sx={{ '&:last-child td, &:last-child th': { border: 0 } }} >
              <TableCell component="th" scope="row">
                {iata}
              </TableCell>              
              <TableCell align="right">{city}</TableCell>
              <TableCell align="right">{state}</TableCell>
              <TableCell align="right">{latitude}</TableCell>
              <TableCell align="right">{longitude}</TableCell>
              <TableCell align="right">{reasonInactive}</TableCell>
              <TableCell align="right"><MySwitch changeReason={setReasonInactive} active={status === 'A'? true : false} iata={iata}/></TableCell>
        </TableRow>
	)
}