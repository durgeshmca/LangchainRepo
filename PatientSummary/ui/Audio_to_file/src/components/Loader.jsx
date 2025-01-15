import React from 'react'

const Loader = () => {
  return (
    <div className='fixed z-[999] flex items-center justify-center w-[100vw] h-[100vh] backdrop-blur-sm bg-transparent '>
        <div className='loader'></div>
    </div>
  )
}

export default Loader