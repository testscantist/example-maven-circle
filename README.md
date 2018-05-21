# Maven/Circle CI Example

Shows a working setup for Circle integration to extract project dependencies

## Circle CI Setup

The `circles.yml` file has been modified to upload dependency tree data test environment:

```yaml
after_success:
  - bash <(curl -s URL)
```
