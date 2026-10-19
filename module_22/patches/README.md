# Optional patches for module 22

Every patch transforms a scratch file named `main.py`. Keep `maze.npy` in the
scratch working directory for window programs and the solution 30 benchmark.

- `patch_22_01_to_02.patch` through `patch_22_22_to_23.patch`: consecutive steps.
- `patch_22_final_to_solution_26.patch` through `patch_22_final_to_solution_30.patch`:
  independent branches from the unmodified final program, not from each other.

The manifest lists each source, target, and target SHA-256. Copy the source file
to `main.py`, run `git apply --check path/to/patch.patch`, then
`git apply path/to/patch.patch`. The result must equal the listed target file.
No Git repository is needed for applying these file patches. Git itself is an
optional development tool, not a runtime dependency of the examples.

Solutions 26–28 open a window. Solutions 29–30 are console experiments; their
patches intentionally change the entry point and may remove unrelated classes.
You can always run the complete target file instead of applying a patch.

Git on Windows may convert LF line endings to CRLF according to local settings.
This does not change the Python program. To preserve exact release bytes and
compare the manifest hashes, use `git -c core.autocrlf=false apply` for that
command only; no global Git setting needs to change.
