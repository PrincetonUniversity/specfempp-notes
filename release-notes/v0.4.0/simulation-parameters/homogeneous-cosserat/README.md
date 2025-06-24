# Wave propagation through homogeneous Cosserat medium with no interfaces

These are the parameters used to create the GIFs in the 0.4.0 release notes

adjust the display parameters to generate different PNGs. For displacement
wavefield:
```yaml
simulation-mode:
      forward:
        writer:
          ...
          display:
            format: PNG
            directory: "OUTPUT_FILES/display"
            field: displacement
            simulation-field: forward
            time-interval: 100
```

for rotation wavefield:
```yaml
simulation-mode:
      forward:
        writer:
          ...
          display:
            format: PNG
            directory: "OUTPUT_FILES/display"
            field: rotation
            simulation-field: forward
            time-interval: 100
...
