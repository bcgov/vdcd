import React, { useState } from 'react';
import Dropzone from 'react-dropzone'
import { useKeycloak } from '@react-keycloak/web';
import useAxios from '../hooks/useAxios'
import Loading from '../components/Loading';
import axios from 'axios';

const Upload = () => {
    const { keycloak } = useKeycloak();
    const redirectUri = `${window.location.origin}/`
    const axiosInstance = useAxios().current;
    
    const [loading, setLoading] = useState(false)
    const [filesToUpload, setFilesToUpload] = useState([])

    const handleSubmit = async () => {
        setLoading(true)

        const putUrlResponse = await axiosInstance.get('/uploaded-vin-records/get_minio_put_url')
        const putUrl = putUrlResponse.data.url
        const object_name = putUrlResponse.data.object_name

        await axios.put(putUrl, filesToUpload[0])
        await axiosInstance.post('/uploaded-vin-records/load_data', {
            object_name
        })

        setFilesToUpload([])
        setLoading(false)
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