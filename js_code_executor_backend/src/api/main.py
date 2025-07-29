from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Any

app = FastAPI(
    title="Flowcode Visual JS Executor API",
    description=(
        "Backend for visual flow diagram-based JavaScript execution. "
        "Provides endpoints to upload and process flow diagrams, securely execute JavaScript code, "
        "and return execution results. All code execution is sandboxed. Auth & error-handling supported."
    ),
    version="0.1.0",
    openapi_tags=[
        {"name": "Flow Diagrams", "description": "Endpoints for submitting flow diagram definitions."},
        {"name": "JS Execution", "description": "Endpoints for executing JavaScript code and returning results."}
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBasic()

# === Models ===

class FlowDiagramRequest(BaseModel):
    """Request model for submitting a flow diagram definition."""
    diagram_json: dict = Field(..., description="The JSON representation of the flow diagram.")

class FlowDiagramResponse(BaseModel):
    """Response after successfully uploading the flow diagram."""
    success: bool = Field(..., description="Status indicator")
    message: str = Field(..., description="Response message")
    diagram_id: Optional[str] = Field(None, description="Unique ID for the stored diagram (if applicable)")

class JSCodeExecutionRequest(BaseModel):
    """Request model for executing JavaScript code."""
    code: str = Field(..., description="JavaScript code to execute, generated from the flow diagram.")
    # Optionally accept diagram_id or context as well in future versions

class JSCodeExecutionResult(BaseModel):
    """Result of the JS code execution."""
    success: bool = Field(..., description="True if the code ran without uncaught errors")
    result: Any = Field(None, description="Result of code execution or error message")
    console: Optional[str] = Field(None, description="Optional: Logs or stdout from execution")
    error_details: Optional[str] = Field(None, description="If failed, error details")

# === Authentication Stub (to be replaced with actual logic) ===

# PUBLIC_INTERFACE
def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Dummy basic authentication (stub). Replace with secure logic.
    """
    # TODO: Replace with actual username/password or API-key check
    if not credentials.username or not credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Auth required",
            headers={"WWW-Authenticate": "Basic"},
        )
    # Optionally: raise if credentials are wrong
    return credentials.username

# === ROUTES ===

@app.get("/", tags=["Health"])
# PUBLIC_INTERFACE
def health_check():
    """Health check endpoint."""
    return {"message": "Healthy"}

@app.post("/api/flowdiagram", response_model=FlowDiagramResponse, tags=["Flow Diagrams"])
# PUBLIC_INTERFACE
def upload_flow_diagram(
    payload: FlowDiagramRequest,
    username: str = Depends(get_current_user)
):
    """
    Accepts a flow diagram definition in JSON format.
    - Validates user authentication (stub).
    - Stores/validates diagram (placeholder), returns a diagram ID.
    """
    # Placeholder logic for storing the flow diagram
    # TODO: Implement actual storage.
    dummy_diagram_id = "dummy-id-12345"
    return FlowDiagramResponse(success=True, message="Flow diagram uploaded.", diagram_id=dummy_diagram_id)

@app.post("/api/execute", response_model=JSCodeExecutionResult, tags=["JS Execution"])
# PUBLIC_INTERFACE
def execute_js_code(
    req: JSCodeExecutionRequest,
    username: str = Depends(get_current_user)
):
    """
    Executes submitted JavaScript code in a sandboxed environment and returns the result.
    - Prepares for secure sandboxed execution (NO inline execution).
    - Handles/logs errors, returns success status and output.
    """
    # === Placeholder: sandboxed execution ===
    try:
        # TODO: Implement secure sandboxed JS execution (e.g., with node.js subprocess via IPC)
        # For now, just return a mock result and do NOT execute input!
        # In production, do not use Python's eval/exec for JS!
        dummy_result = "Execution stub output"
        return JSCodeExecutionResult(success=True, result=dummy_result, console="(no console output)")
    except Exception as ex:
        # Placeholder error handling
        return JSCodeExecutionResult(
            success=False,
            result=None,
            error_details=str(ex),
            console=None
        )

# Handler for 404 and other errors (to demonstrate future-proofing)
@app.exception_handler(Exception)
def generic_exception_handler(request, exc):
    """ Stub for global error handler, demonstrating customizable errors """
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": str(exc), "message": "Internal server error"},
    )
