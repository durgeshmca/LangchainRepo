import axios from 'axios'
import React, { useState } from 'react'
import { AudioRecorder } from 'react-audio-voice-recorder'
import Loader from './components/Loader'

const App = () => {
  const [spokenAudio, setSpokenAudio] = useState(null)
  const [response, setResponse] = useState(null)
  const [loader, setLoader] = useState(false)
  const [details, setDetails] = useState({
    file: null
  })

  const addAudioElement = async blob => {
    const url = URL.createObjectURL(blob)
    setSpokenAudio(url)
    setDetails(pre=>({...pre, file: blob}))
  }

  const handleApiCall = async () => {
    const formData = new FormData()
    formData.append('file', details.file, 'recording.webm')
console.log('import.meta.env.VITE_API_URL', import.meta.env.VITE_API_URL)
    try {
      setLoader(true)
      let { data } = await axios.post(
        `${import.meta.env.VITE_API_URL}/summary`,
        formData
      )
      setResponse(data.message)
    } catch (error) {
      setResponse(JSON.stringify(error))
    }
    finally{
      setLoader(false)
    }
  }

  return (
    <>
      {loader && <Loader />}
      <div className='p-5 flex flex-col gap-6'>
        <div className='flex items-center gap-2'>
          <h1 className='text-[1.2rem] font-[500]'>Speak: </h1>
          <AudioRecorder
            onRecordingComplete={addAudioElement}
            audioTrackConstraints={{
              noiseSuppression: true,
              echoCancellation: true
            }}
            // downloadOnSavePress={true}
            downloadFileExtension='webm'
          />
        </div>

        {spokenAudio && (
          <div className='flex items-center gap-2'>
            <h1 className='text-[1.2rem] font-[500]'>Spoken Audio: </h1>
            <audio src={spokenAudio} controls></audio>
          </div>
        )}

        <button
          onClick={handleApiCall}
          disabled={!details.file}
          className={`border p-2 shadow-md w-[100px] rounded-md ${
            details.file
              ? 'bg-blue-400 text-white cursor-pointer'
              : 'text-slate-600 cursor-not-allowed'
          }`}
        >
          SUBMIT
        </button>

        {response && (
          <div className='flex items-center gap-2'>
            <h1 className='text-[1.2rem] font-[500]'>Response: </h1>
            <p>{response}</p>
          </div>
        )}
      </div>
    </>
  )
}

export default App
