import React from 'react';
import pdf from './about.pdf';

function About() {
  function handleClick() {
    window.open(pdf);
  }

  return (
    <div className='about-button'>
      <button onClick={handleClick}>About</button>
    </div>
  );
}

export default About;
