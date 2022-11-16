import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import { Button, CardActionArea, CardActions } from '@mui/material';
import TextField from '@mui/material/TextField';
import {Paper} from '@mui/material';

function Summ() {
  console.log("HEELLOOEO SENT QUALI")
  return (
    <>
    <div>
    <Card  sx={{ maxWidth: 345 }}>
      <CardActionArea style={{justifyContent:'center'}}>
        <CardContent style={{justifyContent: 'center', alignItems:'center'}}>
        <TextField
          id="filled-multiline-static"
          label="Input Data You Want to Summarize"
          multiline
          rows={4}
          variant="filled"
          style={{width:'100%'}}
        />
        </CardContent>
      </CardActionArea>
      <CardActions style={{justifyContent: 'center'}}>
        <Button size="small" color="success" >
          Submit
        </Button>
      </CardActions>
    </Card>
    <br />
    <Paper elevation={3} style={{width:'21.6rem', textAlign:'center'}} >Get Your Summarized Data
    </Paper>
    </div>
    </>
  );
}

export default Summ;