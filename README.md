# FromDiffuse_To_DenseCloud
Creators: Gema Piedecausa, Jose Manuel Guerrero and Lucas Nicolás Hernández in 2025-26

This code simulates the phase from a diffuse cloud to clusters of dense clouds in the universe. This corresponds to the inicial phases of Protoestellar Formation.
Here are some sheets summarising the proyect: 
https://www.canva.com/design/DAG7gUdG6sA/BZwUen6aumXqcWX4CXBDYQ/edit?utm_content=DAG7gUdG6sA&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton
And the theory used for it is in the pdf "Memory_of_the_proyect.pdf".

The project is divided in two primary enviroments:

# Python Enviroment: Dinamical Simulator
We use the Smooth Particle Hidrodynamics (SPH) for simulating the interaction between "globs" of particles that travel together in the medium. The globs are homogeneous and of mass determined
by the density and volume of the cloud. SPH involes a dampening term with the relative velocity between globs. In order to avoid superposition of the globs by the gravitational attraction, we included
a short-scale Coulomb-Like repulsion force. More information of the simulation, as well as the pertinent references, are included in the pdf "Memory_of_the_proyect.pdf".

****HOW TO USE THE CODE***
1. Tweak the global parameters in "Variables_Globales.py" as desired. Run it to update the variables for the rest of the scripts
2. Be sure to create a folder in the working directory labed "ArchivosPosiciones". This is the default folder for the output of the program. However, it can be changed as it is an optional parameter in Variables_Globales.
   We advise to chose as path the one that overwrites one of the simulators in the unity renderer, such as the example in the last line of the Variables' script.
3. Run Main.py. It should show the progress of the simulation. When ended, the result will be a txt in the path and name chosen that can be read by the Unity Render.


# Unity Enviroment: Renderer
We created a interactable enviroment to analyse the outputs for the simulations. It is built in Unity, but only a build is provided in this repository. Maybe in the future we will upload a version that lets you change the names of each simulation... Sorry!

****HOW TO USE THE SIMULATOR***

1. Check that the simulation that you want to run is properly loaded in the build. This means:
     i) In the build project, check the files in \NubeMolecular_Data\StreamingAssets
     ii) You should see txt labed from 0 to 8. These are the position files that reads each enviroment of the renderer,
         from top left to bottom right.
     iii) Choose one to overwrite with your data. Overwrite it.
2. Open the renderer double-clicking "NubeMolecular.exe". Your OS may ask you to reconfirm that you want to open this unknown program. This means that we probably didnt
   write all the adittional info that can be packed with the build associate with a Company Name, etc. Our original upload (the one in https://github.com/Lucoero/FromDiffuse_To_DenseCloud) is the only one that we can assure it is safe.
3. In the main menu of the simulator, click the button corresponding to your simulation. The renderer can be closed by ALT+F4 (if the default option of ESC is still bugged, again sorry about that).
4. Further instructions are shown in the simulation screen. 
