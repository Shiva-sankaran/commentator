import React from 'react'

export const Button = ({text, color}) => {
  const bgColor = {backgroundColor: color }
  return (
    <div className='button' style={bgColor}> {text} </div>
  )
}

export default Button;