import React, { useContext, useState } from "react"
import { Context } from "../store/appContext"


const ResetPass = () => {
    const [email, setEmail] = useState("")

    const { actions } = useContext(Context)


    const handleChange = ({ target }) => {
        setEmail(target.value)
    }

    const handleSubmit = async (event) => {
        event.preventDefault()

        const response = await actions.resetPassword(email)

    }

    return (
        <div className="container">
            <div className="row justify-content-center">
                <h1 className="text-center">Recuperar la contraseña de la app</h1>
                <div className="col-12 col-md-6 border py-4">
                    <form
                        onSubmit={handleSubmit}
                    >
                        <div className="form-group mb-3">
                            <label htmlFor="lblEmail">Correo Electronico</label>
                            <input
                                className="form-control"
                                placeholder="nombre@email.com"
                                id="lblEmail"
                                name="email"
                                value={email}
                                onChange={handleChange}
                            />
                        </div>
                        <button className="btn btn-outline-primary w-100">Recuperar contraseña</button>
                    </form>
                </div>
            </div>
        </div>
    )
}

export default ResetPass