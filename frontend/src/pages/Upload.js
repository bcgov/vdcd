import React, { useState } from 'react'
import Dropzone from 'react-dropzone'
import useKeycloak from '../hooks/useKeycloak'
import useAxios from '../hooks/useAxios'
import Loading from '../components/Loading'
import Error from '../components/Error'

const Upload = () => {
  const keycloak = useKeycloak()
  const redirectUri = `${window.location.origin}/`
  const axios = useAxios()
  const axiosDefault = useAxios(true)
    
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(false)
  const [filesToUpload, setFilesToUpload] = useState([])

  const handleSubmit = async () => {
    try {
      setLoading(true)

      const putUrlResponse = await axios.get('/uploaded-vin-records/get_minio_put_url')
      const putUrl = putUrlResponse.data.url
      const object_name = putUrlResponse.data.object_name

      await axiosDefault.put(putUrl, filesToUpload[0])
      await axios.post('/uploaded-vin-records/create_file_record', {
        object_name
      })

      setFilesToUpload([])
      setLoading(false)
    } catch (error) {
      setError(true)
    }
  }

  if (error) {
    return <Error/>
  }

  if (loading) {
    return <Loading/>
  }

  return (<div>
    <button
      onClick={()=>{keycloak.logout({ redirectUri })}}
    >
      Logout
    </button>
    <Dropzone
      maxFiles={1}
      onDrop={(files) => {
        setFilesToUpload(files)
      }}
    >
      {({getRootProps, getInputProps}) => (
        <div {...getRootProps()}>
          <input {...getInputProps()} />
          <p>Drag and drop some files here, or click to select files</p>
        </div>
      )}
    </Dropzone>
    {filesToUpload.length > 0 && 
    <div>
      <div>
        File ready to be submitted
      </div>
      <button
        onClick={() => {
          handleSubmit()
        }}
      >
        Submit
      </button>
    </div>}
       
  </div>)
}

export default Upload