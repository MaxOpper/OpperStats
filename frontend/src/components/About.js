import React from 'react';

function About() {
  function handleClick() {
    window.open('https://github.com/MaxOpper/OpperStats');
  }

  return (
    <div className='about-button'>
      <button onClick={handleClick}>About</button>
    </div>
  );
}

export default About;
