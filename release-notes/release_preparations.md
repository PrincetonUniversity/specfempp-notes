# Release Preparations

## Create a draft release on GitHub. 

- Go to the "Releases" section of the repository.
- Click on "Draft a new release".
- Set the tag version (e.g., `v1.0.0`).
- Add a title and description for the release.
- Automatically generate release notes by selecting the "Generate release
  notes" option. We implemented the `./github/release.yaml` and are tagging
  each PR with a supported label.
- Save the draft.

## Create TL;DR

- Manually create a TL;DR section for the release notes highlighting with bullet
  points the most important changes, features, and fixes.

## Create a TL;DR explanations

For some releases you will want to add some examples (e.g, GIF of a simulation,
etc.) and explain the most important changes in more detail. You can only really
do this manually.

## Create Statistics sections

Total commits between the last release and the current one, total number of
```bash
git log --oneline <previous release tag>..<target branch> | wc -l
```

An actual command would look like this for the `devel` branch:
```bash
git log --oneline v0.3.0..devel | wc -l
```

To get the total number of PRs going into the release, we just need to filter the results from above total number of issues
```bash
git log --oneline --grep="Merge pull request" <previous release tag>..<target branch> | wc -l
```
In reality since often we'll do this prior to the release, you can
just use the current branch as the target branch, like so for the `devel` branch:
```bash
git log --oneline --grep="Merge pull request" v0.3.0..devel | wc -l
```


## Create a graph with the number of commits/PRs per week

I let claude create a script for me to analyze the git log and create a graph
with the number of commits and PRs per week, but it was not good enough. I had 
to tweak it a bit to get the output to match the Github style. 

First, get the oneline `git log` and save it to a file:
```bash
git log <prev_release_tag>..main --pretty=format:'"%h","%an","%ad","%s"' > commit_history.csv
```

Then run the script:
```bash
python scripts/commit_analysis.py path/to/SPECFEMPP/commit_history.csv --output ./analysis.png
```

### Creation of simulation GIFs for the release

For the release, we will often include some simulation GIFs to showcase the
changes. The simulations will be run with the
`simulation-mode.forward.writer.display` section in the `specfem_config.yaml`
defined to generate `PNG`. If unsure how to do this, check the
fluid-solid-bathymetry cookbook/benchmark. Once the `PNG` files are generated,
we can use the `magick` command from ImageMagick to automatically crop the images
and create a GIF.
```bash
magick OUTPUT_FILES/display/wavefield*.png -trim +repage -delay 10 -loop 0 wavefield.gif
```
If you want to create a GIF with two side-by-side wavefields (see, cosserat
media release 0.4.0) then you will have to use a two step process:
1. Concatenate snapshots from two separate simulations into a single image using
   ```bash
   mkdir combined
   for i in output_folder1/*.png; do   basename=$(basename "$i");   
       magick "$i" "output_folder2/$basename" -trim +repage +append "combined/$basename"; 
   done;
   ```
   Here we assume that the two output folder contain the same file names since 
   two wavefields are generated with the same setup except for the 
2. Create the GIF from the combined images:
   ```bash
   magick combined/*.png -delay 10 -loop 0 wavefield.gif
   ```

We store parameters for the simulations in this repository for posterity in the
`release-notes/<release #>/simulation_parameters` folders.

To reduce the size of the GIF we can also use `ImageMagick`. Use
```bash
magick original.gif -resize 50% small.gif
```
to reduce the size of the GIF by 50%. There are other options to reduce the size
of the GIF, such as reducing the number of colors, but this is a good starting
point.


