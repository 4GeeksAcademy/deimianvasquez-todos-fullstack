import React, { useContext } from "react"
import { Context } from "../store/appContext"

const Todos = () => {
    const { store } = useContext(Context)

    return (
        <>
            <h1>Hola ¿qué tal {store.currentUser?.name}?</h1>
            <img src={store.currentUser?.avatar} />

        </>
    )
}

export default Todos