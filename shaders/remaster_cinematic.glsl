// Remaster Cinematic Shader for Final Fantasy VIII Recompiled
// Adaptive sharpening + Film-curve tonemapping + Vibrance color enhancement

uniform float u_sharpness;
uniform float u_vibrance;
uniform float u_contrast;

void main() {
    // 1. Center sample and 4-tap cross neighbors
    vec3 cM = textureLod(u_tex, v_uv, 0.0).rgb;
    vec3 cN = textureLod(u_tex, v_uv + vec2(0.0, u_rcp.y), 0.0).rgb;
    vec3 cS = textureLod(u_tex, v_uv - vec2(0.0, u_rcp.y), 0.0).rgb;
    vec3 cE = textureLod(u_tex, v_uv + vec2(u_rcp.x, 0.0), 0.0).rgb;
    vec3 cW = textureLod(u_tex, v_uv - vec2(u_rcp.x, 0.0), 0.0).rgb;

    // 2. Contrast Adaptive Sharpening (CAS)
    // Enhances crisp pre-rendered background detail and character edges without haloing
    vec3 mn = min(min(min(cN, cS), min(cE, cW)), cM);
    vec3 mx = max(max(max(cN, cS), max(cE, cW)), cM);
    vec3 amp = clamp(min(mn, 2.0 - mx) / (mx + 1e-4), 0.0, 1.0);
    vec3 w = -amp * (u_sharpness * 0.25);
    vec3 sharp = (cM + (cN + cS + cE + cW) * w) / (1.0 + 4.0 * w);
    vec3 color = clamp(sharp, 0.0, 1.0);

    // 3. Cinematic Contrast (deepens blacks and brings out midtone punch)
    color = clamp((color - 0.5) * u_contrast + 0.5, 0.0, 1.0);

    // 4. Perceptual Vibrance (boosts washed-out PS1 colors while protecting skin tones)
    float luma = dot(color, vec3(0.299, 0.587, 0.114));
    float max_c = max(color.r, max(color.g, color.b));
    float min_c = min(color.r, min(color.g, color.b));
    float sat = max_c - min_c;
    float boost = (1.0 - sat) * u_vibrance;
    color = mix(vec3(luma), color, 1.0 + boost);

    o = vec4(clamp(color, 0.0, 1.0), 1.0);
}
