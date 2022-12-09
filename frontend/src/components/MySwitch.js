import React from 'react';
import Switch from '@mui/material/Switch'
import axios from "axios"
import { useState} from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';


export default function MySwitch(props) {
  
	
	const airport = props.iata
	const setReason = props.changeReason
	const [active, setActive] = useState(props.active)
	const [open, setOpen] = React.useState(false);
	const [text, setText] = React.useState('')

	const handleClickOpen = () => {
		setText('')
		setOpen(true);
	};

	const handleClose = (confirm) => {
		if (confirm) {
			axios.patch(`http://127.0.0.1:8000/api/toogleInactive/${airport}?reason=${text}`)
			.then(res=> {
				
			})
			setReason(text)
			
			
		} else {
			setActive(!active)
			
				
		}


		setOpen(false);		
	};


	const onClick= () => {
		setActive(!active)
		
		if (active) {
			handleClickOpen()
			
		} else {			
			setReason('')
			axios.patch(`http://127.0.0.1:8000/api/toogleActive/${airport}`)			
		}


		
	}
 
  return(
	<div>
		<Switch checked={active} onChange={()=>onClick()}/>
		
		<Dialog open={open} onClose={handleClose}>
        <DialogTitle>Deactivate Airport</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Please, insert a reason for the Deactivation.
          </DialogContentText>
          <TextField
            autoFocus
            margin="dense"            
            label="Reason"            
            fullWidth
            variant="standard"
			onChange={event => setText(event.target.value)}
			value = {text}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => handleClose(false)}>Cancel</Button>
          <Button onClick={() => handleClose(true)}>Confirm</Button>
        </DialogActions>
      </Dialog>
	</div>
	
  )
}